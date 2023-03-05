"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import openai
import pynecone as pc
openai.api_key = "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" # It doesn't work normally, so insert your own :)


class State(pc.State):
    prompt = ""
    image_url0 = ""
    image_url1 = ""
    image_url2 = ""
    image_url3 = ""
    image_url4 = ""
    image_url5 = ""
    image_url6 = ""
    image_url7 = ""
    진행중 = False
    완료 = False

    def on_process(self):
        self.진행중 = True  # 프로그레스바 나타나게!
        self.완료 = False  # 다음 프롬프트 실행시 이미지 사라지게!

    def get_image(self):
        try:  # <--
            response = openai.Image.create(prompt=self.prompt, n=8, size="256x256")
            self.image_url0 = response["data"][0]["url"]
            self.image_url1 = response["data"][1]["url"]
            self.image_url2 = response["data"][2]["url"]
            self.image_url3 = response["data"][3]["url"]
            self.image_url4 = response["data"][4]["url"]
            self.image_url5 = response["data"][5]["url"]
            self.image_url6 = response["data"][6]["url"]
            self.image_url7 = response["data"][7]["url"]
            self.진행중 = False  # 프로그레스바 사라지게!
            self.완료 = True  # 이미지 나타나게!
        except (openai.error.InvalidRequestError, openai.error.RateLimitError) as e:  # <--
            return pc.window_alert(str(e))


def index():
    return pc.center(
        pc.vstack(
            pc.heading("[Tutorial] DALL-E Web UI", font_size="1.5em"),
            pc.input(placeholder="Enter a prompt..", on_blur=State.set_prompt),
            pc.button("Generate Image", width="100%", on_click=[State.on_process, State.get_image]),
            pc.divider(),
            pc.cond(State.진행중, pc.circular_progress(is_indeterminate=True)),
            pc.cond(State.완료,
                    pc.vstack(
                        pc.hstack(
                            pc.image(src=State.image_url0, height="10em", width="10em", ),
                            pc.image(src=State.image_url1, height="10em", width="10em", ),
                            pc.image(src=State.image_url2, height="10em", width="10em", ),
                            pc.image(src=State.image_url3, height="10em", width="10em", ),
                        ),
                        pc.hstack(
                            pc.image(src=State.image_url4, height="10em", width="10em", ),
                            pc.image(src=State.image_url5, height="10em", width="10em", ),
                            pc.image(src=State.image_url6, height="10em", width="10em", ),
                            pc.image(src=State.image_url7, height="10em", width="10em", ),
                        ),
                    ),
                    ),
            bg="white", padding="2em", shadow="lg", border_radius="lg",
        ),
        width="100%", height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


app = pc.App(state=State)
app.add_page(index, title="Pynecone:DALL-E")
app.compile()