import datetime
from fabric.api import run, env, local
from fabric.context_managers import cd

env.hosts = ['114.215.153.187']
env.user = 'root'
env.password = 'Aiwe2015'


def deploy():
    remote_dir = "/var/www/site/RaPo3/"
    with cd(remote_dir):
        run("git add .")
        run("git commit -m 'server commit {0}'".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        run("git pull origin master")
    remote_dir = "/var/www/site/"
    with cd(remote_dir):
        run("uwsgi --reload uwsgi.pid")


def push(commit, title, desc):
    commit_message = '<{0}> {1}\r\n\r\n{2}'.format(commit, title, desc)
    local("git add .")
    local("git commit -m '{0}'".format(commit_message))
    local("git push origin master")
