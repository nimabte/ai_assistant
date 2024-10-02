import streamlit as st
from PIL import Image
import base64
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage

llm = ChatOpenAI(model="gpt-4o")


def encode_image(upload_file):
    image_bytes = upload_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return base64_image


def gen_response(base64_image, context, input):
    response = llm.invoke(
        [
            AIMessage(
                content=input
            ),
            HumanMessage(
                content=[
                    {"type": "text", "text": context},
                    {"type": "image_url",
                     "image_url": {
                         "url": "data:image/jpg;base64," + base64_image,
                         "detail": "auto"
                     }
                     }
                ]
            )
        ]

    )
    return response.content


def main():
    prompt = """
You are a highly intelligent and helpful assistant who excels at interpreting car manual diagrams and identifying car components shown in images. When given a diagram, please:

Describe what you observe in the diagram.
Explain where each component can be found in the car.
If possible, describe how each item or component looks and provide guidance on how one can locate it.
Mention any specific characteristics that aid in identifying or finding the component.
Ensure your explanations are clear and detailed to assist users in understanding and locating the car components.
    """

    st.title("Car Manual Image Analysis")
    upload_file = st.file_uploader("upload your image here", type=["jpg", "png"])
    if upload_file is not None:
        image = Image.open(upload_file)
        st.image(image, caption="your image", use_column_width=True)
        st.success("image uploaded successfully")
        base64_image = encode_image(upload_file)
        context = st.text_area("Put image context here")
        input = st.text_area("Generation prompt. Edit as you wish:", value=prompt)
        btn = st.button("submit")
        if btn:
            pass
            response = gen_response(base64_image, context, input)
            st.write(response)

if __name__ == '__main__':
    main()

