import { OpenAI } from "openai";

const client = new OpenAI({
  baseURL: "https://router.huggingface.co/novita/v3/openai",
  apiKey: "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",
  dangerouslyAllowBrowser: true,
});

async function translate() {
  const cmd = document.getElementById('cmdName').value.trim();
  if (!cmd) {
    alert('Please enter a command');
    return;
  }

  document.getElementById('result').textContent = 'Loading…';

  try {
    const chatCompletion = await client.chat.completions.create({
      model: "deepseek/deepseek-prover-v2-671b",
      messages: [
        {
          role: "user",
          content: `You are a linux-windows shell command translator. Detect the source operating system (Unix/Linux/macOS or Windows) based on the following command and provide its equivalent for the other operating system.\nCommand: ${cmd}\nReturn only the final command.`,
        },
      ],
    });

    const result = chatCompletion.choices[0].message.content;
    document.getElementById('result').textContent = result || '(no output)';
  } catch (err) {
    document.getElementById('result').textContent = 'Error: ' + err.message;
  }
}

document.getElementById('translateBtn').addEventListener('click', translate);