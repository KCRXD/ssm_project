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
          content: `You are a linux-windows shell command translator. Detect the source operating system (Unix/Linux/macOS or Windows) based on the following command and provide its equivalent for the other operating system.\nCommand: ${cmd}\nReturn only the final command.
          keep the command as short as possible and do not add any explanation or additional text.\n
          ONLY ANSWER with ONE LINERS!`
          ,
          
        },
      ],
    });

    const result = chatCompletion.choices[0].message.content;
    document.getElementById('result').textContent = result || '(no output)';
  } catch (err) {
    console.error("Error during API call:", err);
    document.getElementById('result').textContent = 'Error: ' + err.message;
  }
}

document.getElementById('translateBtn').addEventListener('click', translate);