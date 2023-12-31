from substrateinterface import SubstrateInterface, Keypair

from .examples import create_data_annotator_task, create_model_contributor_task, create_model_engineer_task
from .assign_task import assign_task
from .send_task_result import send_task_result
from .storage_ipfs import get_result_path

from .settings import SOCKET_URL, ASSETS_FOLDER
from .storage import upload_data_to_remote, download_data_from_remote, upload_results_to_remote

class ModelCreator:
    def __init__(self) -> None:
        self

    @classmethod
    def create_task_data_ann(cls):
        task_id = create_data_annotator_task()
        upload_data_to_remote("data_annotator", task_id)
    
    @classmethod
    def create_task_model_contr(cls):
        task_id = create_model_contributor_task()
        upload_data_to_remote("model_contributor", task_id)

    @classmethod
    def create_task_model_eng(cls):
        task_id = create_model_engineer_task()
        upload_data_to_remote("model_engineer", task_id)

    @classmethod
    def menu(cls):
        choice = -1
        while choice != 5:
            print("Choose your command")
            print(f"\t1\t-\tCreate task")
            print(f"\t2\t-\tList tasks")
            print(f"\t3\t-\tList tasks results")
            print(f"\t4\t-\tAccept task results")
            print(f"\t4\t-\tReject task results")
            print(f"\t5\t-\tExit")
            try:
                choice = int(input())
                match choice:
                    case 1:
                        subchoice = -1
                        while subchoice != 4:
                            print("What kind of task you want to create")
                            print(f"\t1\t-\tData annotator")
                            print(f"\t2\t-\tModel contributor")
                            print(f"\t3\t-\tModel engineer")
                            print(f"\t4\t-\tCancel")
                            try:
                                subchoice = int(input())
                            except ValueError as e:
                                print("Choice must be one value in the interval [1-4]")
                                subchoice = -1
                            match subchoice:
                                case 1:
                                    ModelCreator.create_task_data_ann()
                                    subchoice = 4
                                case 2:
                                    ModelCreator.create_task_model_contr()
                                    subchoice = 4
                                case 3:
                                    ModelCreator.create_task_model_eng()
                                    subchoice = 4
                                case _:
                                    print("Choice must be one value in the interval [1-4]")
                                    subchoice = -1
                    case 2:
                        pass
            except ValueError as e:
                print("Choice must be one value in the interval [1-5]")
                choice = -1

    @classmethod
    def validate_task_results(cls):
        pass
    
    @classmethod
    def accept_task_results(cls):
        pass
    
    @classmethod
    def reject_task_results():
        pass


class Contributor():

    def __init__(self, role) -> None:
        self.role = role
    
    @classmethod
    def assign_task(cls, task_id=1):
        download_data_from_remote(cls.role, task_id)

        substrate = SubstrateInterface(url=SOCKET_URL)
        passphrase = None  # Replace with actual passphrase or keep as None to use sudoaccount

        # Determine the account to use based on passphrase availability
        if passphrase:
            assign_task(substrate, None, passphrase, task_id)
        else:
            alice = Keypair.create_from_uri('//Alice')
            assign_task(substrate, alice, None, task_id)
    
    @classmethod
    def run_task(cls, task_id=1):
        print(f"To execute the task, use the script in: {ASSETS_FOLDER}/{task_id}/{cls.role}")
        print("Once you are done, use the 'Send task results' option in this application")

    @classmethod
    def send_task_results(cls, task_id=1):
        upload_results_to_remote(cls.role, task_id)

        substrate = SubstrateInterface(url=SOCKET_URL)
        passphrase = None  # Assuming no passphrase is provided

        # Sample data for sending task result
        submission_id = 1  # Example submission ID
        result = "result_labels_or_weights_string"
        result_path = get_result_path()  # file with the weights  
        result_storage_type = "IPFS"
        result_storage_credentials = "ipfs_access_credentials"

        # Determine the account to use based on passphrase availability
        if passphrase:
            keypair = Keypair.create_from_mnemonic(passphrase)
        else:
            keypair = Keypair.create_from_uri('//Alice')

        send_task_result(substrate, keypair, submission_id, result, result_path, result_storage_type, result_storage_credentials)

    @classmethod
    def menu(cls):
        choice = -1
        while choice != 5:
            print("Choose your command")
            print(f"\t1\t-\tList tasks")
            print(f"\t2\t-\tAssign tasks")
            print(f"\t3\t-\tExecute tasks")
            print(f"\t4\t-\tSend tasks results")
            print(f"\t5\t-\tExit")
            try:
                choice = int(input())
                match choice:
                    case 1:
                        pass
                    case 2:
                        task_id = int(input("Input id of task to accept\n"))
                        cls.assign_task(task_id)
                    case 3:
                        cls.run_task()
                    case 4:
                        cls.send_task_results()
                    
            except ValueError as e:
                print("Choice must be one value in the interval [1-5]")
                choice = -1


class ModelContributor(Contributor):
    role = "model_contributor"

    def __init__(self) -> None:
        super.__init__()


class DataAnnotator(Contributor):
    role = "data_annotator"

    def __init__(self) -> None:
        super.__init__()

class ModelEngineer(Contributor):
    role = "model_engineer"

    def __init__(self) -> None:
        super.__init__()
    