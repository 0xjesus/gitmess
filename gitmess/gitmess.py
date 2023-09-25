import git
import logging
import os
import argparse
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
logging.basicConfig(level=logging.ERROR)

openai_key = os.getenv("OPEN_AI_KEY")
chat_model = ChatOpenAI(
    model="gpt-3.5-turbo"
)
LIBRARY_VERSION = "0.1.0"  # Remember to update this version as needed.

def get_args():
    parser = argparse.ArgumentParser(description="Git helper using OpenAI.")
    parser.add_argument('-v', '--version', action='store_true', help="Show library version and exit.")
    parser.add_argument('--push-auto', action='store_true', help="Ask to confirm auto push after committing.")
    return parser.parse_args()

def fetch_git_changes(repo_path=".", push_auto=False):
    try:
        system_message = """
            You are a helpful assistant the produce always as output a commit message using the standar of https://www.conventionalcommits.org/en/v1.0.0/.
            Do not include author info, just include a list describing the changes with the following format <emoji> <type>(<scope>): <short summary>. 
            example: 🐛 fix(gitmess): Fix typo in commit message format. Do not duplicate messages.
            To formulate your output you will have access to the giff in the following text provided by the git diff command.
        """
        messages = [
            SystemMessage(content=f"{system_message}"),
        ]
        # Abrir el repositorio
        repo = git.Repo(repo_path)
        # Obtener las diferencias con respecto a la última confirmación
        # Si quieres comparar con otra referencia, puedes cambiar 'HEAD'
        diff = repo.git.diff('HEAD')
        if diff:
            messages.append(SystemMessage(content=f"{diff}"))
            ## print a beautiful animation while the model is thinking
            print("Analyzing...🤔")
            response = chat_model.predict_messages(messages).content
            ## clear the last print
            print("\033[A                             \033[A")

            ## ask the user for confirmation of the message at the console
            print(response)
            ## ask the user for confirmation of the message at the console
            user_input = input("\nIs the message correct? [Y/n] ")
            if user_input.lower() == "y":
                ## commit the changes
                repo.git.add(update=True)
                repo.git.commit(message=response)
                if push_auto or input("\nDo you want to push the changes? [Y/n] ").lower() == "y":
                    repo.git.push()
                    print(repo.git.log('--oneline', '-n', '1'))
                    return f"\nCommit generated and pushed successfully"
                else:
                    return f"Commit generated successfully"
            else:
                return "Commit canceled"
        return diff if diff else "No changes"
    except Exception as e:
        raise e


if __name__ == "__main__":
    args = get_args()

    # Si el usuario sólo quiere ver la versión
    if args.version:
        print(f"📜 Gitmess version: {LIBRARY_VERSION}")
        exit()

    # Si el usuario activa el flag de push-auto
    if args.push_auto:
        confirmation = input("You've chosen to auto-push. Are you sure you want to enable this? [Y/n] ")
        if confirmation.lower() == 'n':
            args.push_auto = False

    # Si el usuario no ha proporcionado ningún argumento, ejecuta fetch_git_changes
    if not any(vars(args).values()):
        print(fetch_git_changes(push_auto=args.push_auto))

