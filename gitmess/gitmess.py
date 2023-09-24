import git
import logging
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
logging.basicConfig(level=logging.ERROR)

openai_key = os.getenv("OPEN_AI_KEY")
chat_model = ChatOpenAI(
    model="gpt-3.5-turbo"
)

def fetch_git_changes(repo_path="."):
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
                ## ask the user if he wants to push the changes
                user_input = input("\nDo you want to push the changes? [Y/n] ")
                if user_input.lower() == "y":
                    repo.git.push()
                    ## show the output of the push
                    print(repo.git.log('--oneline', '-n', '1'))
                    return f"\nCommit generated and pushed successfully"
                else:
                    return f"Commit generated successfully"
            else:
                return "Commit canceled"
        return diff if diff else "No changes"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Imprimir las diferencias
    print(fetch_git_changes())
