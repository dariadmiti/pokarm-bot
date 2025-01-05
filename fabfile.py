from fabric import Connection, task


project_dir = "~/pokarm-bot"


@task
def sync_repo(context):
    conn = Connection("pokarm-bot")
    if conn.run(f"test -d {project_dir}", warn=True).failed:
        print("Cloning git repository")
        conn.run(
            f"git clone https://github.com/dariadmiti/pokarm-bot.git {project_dir}",
            echo=True,
        )
    else:
        print("Pulling git repository")
        with conn.cd(project_dir):
            conn.run("git pull origin", echo=True)


@task
def deploy(context):
    sync_repo(context)
