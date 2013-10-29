import requests
import json

class CloudFacadeInterface():
    """ The CloudFacadeInterface allows the creation, managements and destruction of workflows in the cloudfacade """
   
    def __init__(self, cfURL):
        """ Initializes the manager

        Arguments:
            cfURL (string): the url of the cloudfacade API

        """
        self.CLOUDFACACE_URL = cfURL

    def createWorkflow(self, ticket):
        """ Creates a new workflow in the cloudfacade

        Arguments:
            ticket (string): a valid authentication ticket

        Returns:
            dictionary::

                Success -- {'workflowId':'a string value'}
                Failure -- {'workflowId':'', 'error.description':'', error.code:''}

        """
        ret = {}
        try:
            body = json.dumps({'name': "tavernaserverworkflow", 'type':  "workflow"})
            con = requests.post(
                "%s/workflows" % self.CLOUDFACACE_URL,
                auth=("", ticket),
                data = body, 
                verify = False
            )

            if con.status_code != 200:
                ret["workflowId"] = ""
                ret["error.description"] = "Error creating workflow"
                ret["error.code"] = con.status_code

            ret["workflowId"] = con.text

        except Exception as e:
            ret["workflowId"] = ""
            ret["error.description"] = "Error creating workflow"
            ret["error.code"] = e

        return ret


    def deleteWorkflow(self,  workflowId, ticket):
        """ Deletes the workflow with id workflowId from the cloudfacade

        Arguments:
            workflowId (string): a valid id for a workflow in the cloudfacade

            ticket (string): a valid authentication ticket

        Returns:
            dictionary::

                Success -- {'workflowId':'a string value'}
                Failure -- {'workflowId':'', 'error.description':'', error.code:''}

        """
        ret = {}
        try:
            ret["workflowId"] = workflowId
            con = requests.delete(
                "%s/workflows/%s" % (self.CLOUDFACACE_URL, workflowId),
                auth=("", ticket),
                verify = False
            )
            if con.status_code != 200 and con.status_code != 204:
                ret["workflowId"] = ""
                ret["error.description"] = "Error deleting workflow " + workflowId
                ret["error.code"] = con.status_code

        except Exception as e:
            ret["workflowId"] = ""
            ret["error.description"] = "Error deleting workflow " + workflowId
            ret["error.code"] = e

        return ret



    def getAtomicServiceConfigId(self, atomicServiceId, ticket):
        """ Retrieves the service configuration Id of an AS

        Arguments:
            atomicServiceId (string): a valid id for an atomic service in the cloudfacade

            ticket (string): a valid authentication ticket

        Returns:
            dictionary::

                Success -- {'asConfigId':'a string value'}
                Failure -- {'asConfigId':'', 'error.description':'', error.code:''}

        """
        ret = {}
        try:
            con = requests.get(
                "%s/atomic_services/%s/configurations" % (self.CLOUDFACACE_URL, atomicServiceId),
                auth=("", ticket),
               verify = False
            )

            if con.status_code != 200:
                ret["asConfigId"] = ""
                ret["error.description"] = "Error getting configuration Id for AS " + atomicServiceId
                ret["error.code"] = con.status_code

            json = con.json()
            ret["asConfigId"] = json[0]["id"]

        except Exception as e:
            ret["asConfigId"] = ""
            ret["error.description"] = "Error getting configuration Id for AS " + atomicServiceId
            ret["error.code"] = e

        return ret



    def startAtomicService(self, atomicServiceConfigId, workflowId, ticket):
        """ Adds an atomic service to a workflow 

        Arguments:
           workflowId (string): a valid id for a workflow in the cloudfacade

           atomicServiceConfigId (string): a valid atomic service configuration id in the cloudfacade

           ticket (string): a valid authentication ticket

        Returns:
            dictionary::

                Success -- {'workflowId':'a string value'}
                Failure -- {'workflowId':'', 'error.description':'', error.code:''}

        """
        ret = {}
        try:
            ret["workflowId"] = workflowId
            body = json.dumps( {'asConfigId':  atomicServiceConfigId} )
            con = requests.post(
                "%s/workflows/%s/atomic_services" % (self.CLOUDFACACE_URL, workflowId),
                auth=("", ticket),
                data = body, 
                verify = False
            )
            if con.status_code != 200:
                ret["workflowId"] = ""
                ret["error.description"] = "Error starting Taverna Server in workflow " + workflowId
                ret["error.code"] = con.status_code
                
        except Exception as e:
            ret["workflowId"] = ""
            ret["error.description"] = "Error starting Taverna Server in workflow " + workflowId
            ret["error.code"] = e

        return ret



    def getASwebEndpoint(self, atomicServiceConfigId, workflowId, ticket):
        """ Retrieves the web endpoint URL of an atomic service 

        Arguments:
           workflowId (string): a valid id for a workflow in the cloudfacade

           atomicServiceConfigId (string): a valid atomic service configuration id in the cloudfacade

           ticket (string): a valid authentication ticket

        Returns:
            dictionary::

                Success -- {'endpoint':'a string value'}
                Failure -- {'endpoint':'', 'error.description':'', error.code:''}

        """
        ret = {}
        try:
            ret["workflowId"] = workflowId
            url = "null"
            while url.find("null")!=-1:
                con = requests.get(
                    "%s/workflows/%s/atomic_services/%s/redirections" % (self.CLOUDFACACE_URL, workflowId, atomicServiceConfigId ),
                    auth=("", ticket),
                    verify = False
                    )
                json = con.json()
                if json["http"][0]["urls"][0].find("null")==-1:
                    url = json["http"][0]["urls"][0]

            ret["endpoint"] = url

        except Exception as e:
            ret["endpoint"] = ""
            ret["error.description"] = "Error getting Taverna Server endpoint in workflow " + workflowId
            ret["error.code"] = e

        return ret



    def isWebEndpointReady(self, url, username, password):
        """ Checks if the web endpoint at URL is reachable

        Arguments:
            url (string): a valid endpoint url 

            ticket (string): a valid authentication ticket

        Returns:
            True is a successful connection was made to the endpoint. It returns False otherwise.
            

        """
        if url:
            con = requests.get( 
                url,
                auth=(username, password),
                verify = False
                )
            if con.status_code == 200:
                return True
        return False;