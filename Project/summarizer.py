from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

pre_prompt = """
                너는 회의록을 정리하는 서기야. 아래의 Markdown 형식에 맞춰 회의 내용을 요약해줘.
                각 항목은 모두 Markdown 형식이어야 해. 각 내용은 개괄식으로 형식 잘 맞춰서 작성해.
             """

def generate_minutes(customized_prompt, text_to_summarize):
    """ Generates the summary of the `text_to_summarize` with the template given by `customized_prompt`.

    Args:
        customized_prompt (string): Customized prompt for GPT from the user, including the template for this minute, etc.
        text_to_summarize (string): Text to be organized by `customized_prompt`.

    Returns:
        string: Generated minute with the template of user's customization.
    """    
    print(">> generating response..")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
        {"role": "system", "content": pre_prompt+customized_prompt},
        {"role": "user", "content": text_to_summarize}
        ]
    )

    return completion.choices[0].message.content
