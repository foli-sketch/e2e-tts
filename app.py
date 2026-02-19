import gradio as gr
from synthesizer import Synthesizer
from languages import TTS_LANGUAGES


# Initialize synthesizer
synthesizer = Synthesizer()


def format_languages():
    """
    Convert dictionary to dropdown format.
    Example: en (English)
    """
    return [f"{code} ({name})" for code, name in TTS_LANGUAGES.items()]


def extract_language_code(selection):
    """
    Extract language code safely from dropdown selection.
    """
    if "(" in selection:
        return selection.split(" ")[0]
    return selection


def synthesize_text(text, language):
    """
    Main synthesis function with safe error handling.
    """
    try:
        if not text:
            return None

        lang_code = extract_language_code(language)
        audio_path = synthesizer.synthesis(text, lang_code)
        return audio_path

    except Exception as e:
        print("Synthesis Error:", str(e))
        return None


# Ensure at least one language exists
if not TTS_LANGUAGES:
    raise ValueError("TTS_LANGUAGES dictionary is empty.")


default_lang_code = list(TTS_LANGUAGES.keys())[0]
default_lang_name = TTS_LANGUAGES[default_lang_code]


# Simple example (dynamic)
TTS_EXAMPLES = [
    [f"This is a demo for {default_lang_name}.",
     f"{default_lang_code} ({default_lang_name})"]
]


# Create Gradio interface
app = gr.Interface(
    fn=synthesize_text,
    inputs=[
        gr.Textbox(label="Input Text"),
        gr.Dropdown(
            choices=format_languages(),
            value=f"{default_lang_code} ({default_lang_name})",
            label="Language"
        )
    ],
    outputs=gr.Audio(label="Synthesized Audio", type="filepath"),
    examples=TTS_EXAMPLES,
    title="Interlink AI - Text to Speech",
    description="Generate high-quality speech from text.",
    allow_flagging="never"
)


if __name__ == "__main__":
    app.launch()
