```
[root@m01 untitled]# celery -A untitled worker -l info
/usr/local/python3/lib/python3.6/site-packages/celery/platforms.py:801: RuntimeWarning: You're running the worker with superuser privileges: this is
absolutely not recommended!

Please specify a different user using the --uid option.

User information: uid=0 euid=0 gid=0 egid=0

  uid=uid, euid=euid, gid=gid, egid=egid,
 
 -------------- celery@m01 v4.3.0 (rhubarb)
---- **** ----- 
--- * ***  * -- Linux-2.6.32-696.el6.x86_64-x86_64-with-centos-6.9-Final 2019-07-18 13:13:52
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         untitled:0x7fa14a5312e8
- ** ---------- .> transport:   redis://10.0.0.61:6379/2
- ** ---------- .> results:     
- *** --- * --- .> concurrency: 2 (prefork)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . printqw

[2019-07-18 13:13:52,288: INFO/MainProcess] Connected to redis://10.0.0.61:6379/2
[2019-07-18 13:13:52,297: INFO/MainProcess] mingle: searching for neighbors
[2019-07-18 13:13:53,319: INFO/MainProcess] mingle: all alone
[2019-07-18 13:13:53,330: WARNING/MainProcess] /usr/local/python3/lib/python3.6/site-packages/celery/fixups/django.py:202: UserWarning: Using settings.DEBUG leads to a memory leak, never use this setting in production environments!
  warnings.warn('Using settings.DEBUG leads to a memory leak, never '
[2019-07-18 13:13:53,331: INFO/MainProcess] celery@m01 ready.
[2019-07-18 13:13:53,448: INFO/MainProcess] Received task: printqw[e3d1792f-7628-4861-9fc7-05fd8e7ce537]  
[2019-07-18 13:13:53,469: INFO/ForkPoolWorker-1] Task printqw[e3d1792f-7628-4861-9fc7-05fd8e7ce537] succeeded in 0.01883281399932457s: 'hello celery and django...'
[2019-07-18 13:13:53,969: INFO/MainProcess] Received task: printqw[b874cb79-4aac-4b09-a9f8-5906bf09326b]  
[2019-07-18 13:13:53,979: INFO/ForkPoolWorker-1] Task printqw[b874cb79-4aac-4b09-a9f8-5906bf09326b] succeeded in 0.009641711996664526s: 'hello celery and django...'

```
```
[root@m01 untitled]# celery -A untitled beat -l info
celery beat v4.3.0 (rhubarb) is starting.
__    -    ... __   -        _
LocalTime -> 2019-07-18 13:13:48
Configuration ->
    . broker -> redis://10.0.0.61:6379/2
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> celery.beat.PersistentScheduler
    . db -> celerybeat-schedule
    . logfile -> [stderr]@%INFO
    . maxinterval -> 5.00 minutes (300s)
[2019-07-18 13:13:48,957: INFO/MainProcess] beat: Starting...
[2019-07-18 13:13:48,978: INFO/MainProcess] Scheduler: Sending due task task-one (printqw)
[2019-07-18 13:13:53,967: INFO/MainProcess] Scheduler: Sending due task task-one (printqw)

```