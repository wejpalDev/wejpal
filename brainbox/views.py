from django.shortcuts import render
from rest_framework import generics
from .serializers import InputSerializer
from rest_framework.response import Response
from rest_framework import status
import openai
from langchain import OpenAI
import requests
from langchain import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import os

class GenerateValidateView(generics.GenericAPIView):
    serializer_class = InputSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            os.environ['OPENAI_API_KEY'] = "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"
            davinci = OpenAI(model_name="text-davinci-003")

            api_key = '400edd51438e5859e9ed259ee62b0673f7dcff223f83e87ec914e538f53170c3'

            query= serializer.data["prompt"]
            # Set up the API endpoint URL
            base_url = 'https://serpapi.com/search'
            params = {
                'q': query,
                'api_key': api_key,
                # Add any additional parameters as needed
            }

            # Make the GET request
            response = requests.get(base_url, params=params)

            value = response.json()

            # print(value["related_questions"])

            h = ""

            for i in value["organic_results"]:

                if "snippet" in i:
                    h = h + i["snippet"]

            prompt = """
                        Answer the question based on the context below. Start your answer with either Yes or No, but give a good explanation"

                        Context: {context}

                        Question: {query}

                        Answer: """

            prompt_template = PromptTemplate(
                input_variables=["query", "context"],
                template=prompt
            )


            print(h)
            message = davinci(prompt_template.format(
                query=query,
                context=h))



            if "Yes" in message:
                    result =  {
                        "isTrue":'true',
                    "response_1": message}
            else:
                result = {
                    "isTrue": 'false',
                    "response_1": message}

            return Response(
                result,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


def reformatQuery(original_string):
    modified_string = original_string.replace(" ", "+")
    return modified_string




