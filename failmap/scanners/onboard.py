import logging

from celery import group
from django.utils import timezone

from failmap.organizations.models import Url
from failmap.scanners.tasks import (DEFAULT_CRAWLERS, DEFAULT_ONBOARDERS, DEFAULT_SCANNERS,
                                    TLD_DEFAULT_CRAWLERS, TLD_DEFAULT_ONBOARDERS,
                                    TLD_DEFAULT_SCANNERS)

from ..celery import Task, app

log = logging.getLogger(__package__)


def compose_task(
    organizations_filter: dict = dict(),
    urls_filter: dict = dict(),
    endpoints_filter: dict = dict(),
) -> Task:
    """Compose taskset to onboard specified urls."""

    urls = Url.objects.filter(**urls_filter)

    if not urls:
        raise Exception('Applied filters resulted in no tasks!')

    log.info('Creating onboard task for %s urls.', len(urls))

    tasks = []
    for url in urls:
        crawl = compose_crawl_tasks(url)
        explore = compose_explore_tasks(url)
        # We made a mistake in the chain: the scanner tasks can only run IF there are endpoints.
        # and the chain with scan_tasks does not wait until the explore tasks are finished.
        # The explore tasks discover endoints (and save them).
        # Without explore tasks there are no endpoints, so all scanners fail.
        # But moving to a chord seems to be hard/impossible. I'm getting a
        # self Error in formatting: TypeError: 'AsyncResult' object is not subscriptable
        # Error in formatting: TypeError: 'AsyncResult' object is not subscriptable
        # https://stackoverflow.com/questions/47457546/

        task_str = str(explore)
        task_str = task_str.replace("), group(", "), \n group(")
        task_str = task_str.replace("|", "\n|")
        print(task_str)

        if crawl:
            tasks.append(explore | crawl | finish_onboarding.si(url) | scan_tasks.si(url))
        else:
            # scan task may have no ednpoints, we're not going to give exceptions anymore...
            tasks.append(explore | (dummy_task.si() | finish_onboarding_mutable.s(url) | scan_tasks.si(url)))

    task = group(tasks)

    # Trying to make the output gibberish more readable.
    task_str = str(tasks)
    task_str = task_str.replace("), group(", "), \n group(")
    task_str = task_str.replace("|", "\n|")
    print(task_str)

    # keeping a raw version
    # print("Tasks:")
    # print(task)

    return task


@app.task(queue='storage')
def dummy_task():
    log.error("Nothing is going wrong here...")


def compose_explore_tasks(url):
    """Return tasks to explore urls and endpoints for a given url."""

    onboarders = DEFAULT_ONBOARDERS
    if url.is_top_level():
        onboarders += TLD_DEFAULT_ONBOARDERS

    tasks = []
    for onboarder in onboarders:
        tasks.append(onboarder(urls_filter={"url": url}))

    return group(tasks)


def compose_crawl_tasks(url):

    crawlers = DEFAULT_CRAWLERS
    if url.is_top_level():
        crawlers += TLD_DEFAULT_CRAWLERS

    tasks = []
    for crawler in crawlers:
        tasks.append(crawler(urls_filter={"url": url}))

    return group(tasks)


@app.task(queue='storage')
def scan_tasks(url):
    """Put tasks on the queue to do an initial scan for all relevant scanners.

    This tasks is to be called after onboarding has finished and as then url endpoints are available.
    """

    scanners = DEFAULT_SCANNERS
    if url.is_top_level():
        scanners += TLD_DEFAULT_SCANNERS

    tasks = []
    for scanner in scanners:
        tasks.append(scanner(urls_filter={"url": url}))

    log.info(tasks)

    group(tasks).apply_async()


@app.task(queue='storage')
def finish_onboarding(url):
    log.info("Finishing onboarding of %s", url)
    url.onboarded = True
    url.onboarded_on = timezone.now()
    url.save(update_fields=['onboarded_on', 'onboarded'])

    return True


@app.task(queue='storage')
def finish_onboarding_mutable(result, url):
    log.info("Finishing onboarding of %s", url)
    url.onboarded = True
    url.onboarded_on = timezone.now()
    url.save(update_fields=['onboarded_on', 'onboarded'])

    return True
