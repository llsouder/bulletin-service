# bulletin-service

Code taken from this tutorial:
https://keathmilligan.net/automate-your-work-with-msgraph-and-python

## Redeploy live site:

### Git push

    git push -f azure <local_branch>:master

### Azure command line

too complicated. does not work consistently.

    az webapp up --name bulletin-service --plan lonnie.souder_asp_Linux_centralus__1 --location eastus2
