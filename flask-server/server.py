from flask import Flask
import os
import langchain.chat_models as chat_models
import langchain.chains as chains
import langchain.graphs as graphs

os.environ['OPENAI_API_KEY'] = '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'


app = Flask(__name__)


@app.route("/")
def hello_world():
    return 'Hello World'

@app.route("/members")
def members():
    return {"members":["m1", "m2", "m3"]}

@app.route("/chatbot/<question>")
def respond_to_question(question):
  """Responds to the user's question by using the GraphSparqlQAChain model."""
  graph = graphs.RdfGraph(
      source_file="./test.ttl",
      standard="rdf",
      local_copy="test.ttl",
  )
  chain = chains.GraphSparqlQAChain.from_llm(
      chat_models.ChatOpenAI(temperature=0), graph=graph, verbose=True
  )
  answer = chain.run(question)
  return {
        "answer": answer,
        "direction": "incoming",
        "sender": "ChatGPT"
    }

if __name__ == "__main__":
    app.run(debug=True)