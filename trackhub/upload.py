import os
from fabric.api import local, settings, run, abort, cd, env, hide, put
from fabric.contrib.console import confirm


def upload_file(host, user, local_fn, remote_fn, port=22,
                rsync_options='-azvr --progress', run_local=False):
    results = []
    if run_local:
        if not os.path.exists(os.path.dirname(remote_fn)):
            results.append(local('mkdir -p %s' % os.path.dirname(remote_fn)))

        results.append(local('rsync -avr --progress %(local_fn)s %(remote_fn)s' % locals()))
        return results
    env.host_string = host
    env.user = user
    env.port = port

    remote_dir = os.path.dirname(remote_fn)

    with settings(warn_only=True):
        result = run('ls %s' % remote_dir)

    if result.failed:
        run('mkdir -p %s' % remote_dir)

    rsync_template = \
        'rsync %(rsync_options)s %(local_fn)s %(user)s@%(host)s:%(remote_fn)s'
    with settings(warn_only=True):
        results.append(local(rsync_template % locals()))
    return results


def upload_hub(host, user, hub, port=22, rsync_options='-azvr --progress',
               run_local=False):
    kwargs = dict(host=host, user=user, port=port, rsync_options=rsync_options,
                  run_local=run_local)
    print kwargs
    results = []

    # First the hub file:
    results.extend(
        upload_file(
            local_fn=hub.local_fn,
            remote_fn=hub.remote_fn,
            **kwargs)
    )

    # Then the genomes file:
    print hub.genomes_file.local_fn
    results.extend(
        upload_file(
            local_fn=hub.genomes_file.local_fn,
            remote_fn=hub.genomes_file.remote_fn,
            **kwargs)
    )

    # And finally the trackDB file:
    for g in hub.genomes_file.genomes:
        results.extend(
            upload_file(
                local_fn=g.trackdb.local_fn,
                remote_fn=g.trackdb.remote_fn,
                **kwargs
            )
        )
    return results


def upload_track(host, user, track, port=22, rsync_options='-azvr --progress',
                 run_local=False):
    kwargs = dict(host=host, user=user, local_fn=track.local_fn,
                  remote_fn=track.remote_fn, rsync_options=rsync_options,
                  run_local=run_local)
    results = upload_file(**kwargs)
    if track.tracktype == 'bam':
        kwargs['local_fn'] += '.bai'
        results.extend(upload_file(**kwargs))
    return results
