async function apiRequest(path, payload) {
  const response = await fetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Request failed');
  }

  return data;
}

function renderOutput(elementId, htmlContent) {
  const output = document.getElementById(elementId);
  output.innerHTML = htmlContent;
}

document.getElementById('qa-btn').addEventListener('click', async () => {
  const question = document.getElementById('qa-question').value.trim();
  if (!question) {
    renderOutput('qa-output', '<p>Please enter a question.</p>');
    return;
  }

  try {
    const data = await apiRequest('/qa', { question });
    renderOutput('qa-output', `<p>${data.answer}</p>`);
  } catch (error) {
    renderOutput('qa-output', `<p class="error">${error.message}</p>`);
  }
});

document.getElementById('explain-btn').addEventListener('click', async () => {
  const topic = document.getElementById('explain-topic').value.trim();
  const level = document.getElementById('explain-level').value;

  if (!topic) {
    renderOutput('explain-output', '<p>Please enter a topic.</p>');
    return;
  }

  try {
    const data = await apiRequest('/explain', { topic, level });
    renderOutput('explain-output', `<p>${data.explanation}</p>`);
  } catch (error) {
    renderOutput('explain-output', `<p class="error">${error.message}</p>`);
  }
});

document.getElementById('summary-btn').addEventListener('click', async () => {
  const text = document.getElementById('summary-text').value.trim();
  const max_bullets = Number(document.getElementById('summary-bullets').value || 5);

  if (!text) {
    renderOutput('summary-output', '<p>Please enter text to summarize.</p>');
    return;
  }

  try {
    const data = await apiRequest('/summarize', { text, max_bullets });
    renderOutput('summary-output', `<pre>${data.summary}</pre>`);
  } catch (error) {
    renderOutput('summary-output', `<p class="error">${error.message}</p>`);
  }
});

document.getElementById('quiz-btn').addEventListener('click', async () => {
  const content = document.getElementById('quiz-content').value.trim();
  const count = Number(document.getElementById('quiz-count').value || 5);

  if (!content) {
    renderOutput('quiz-output', '<p>Please enter content for the quiz.</p>');
    return;
  }

  try {
    const data = await apiRequest('/quiz', { content, count });
    const questions = data.questions || [];
    const html = questions.map((q, index) => `
      <div class="question-block">
        <p><strong>${index + 1}. ${q.question}</strong></p>
        <ul>
          ${q.options.map((option) => `<li>${option}</li>`).join('')}
        </ul>
        <p>Answer: ${q.correct_answer}</p>
        <p>${q.explanation}</p>
      </div>
    `).join('');
    renderOutput('quiz-output', html || '<p>No quiz generated.</p>');
  } catch (error) {
    renderOutput('quiz-output', `<p class="error">${error.message}</p>`);
  }
});

document.getElementById('learn-btn').addEventListener('click', async () => {
  const topic = document.getElementById('learn-topic').value.trim();
  const level = document.getElementById('learn-level').value;
  const weeks = Number(document.getElementById('learn-weeks').value || 4);

  if (!topic) {
    renderOutput('learn-output', '<p>Please enter a topic.</p>');
    return;
  }

  try {
    const data = await apiRequest('/learn/recommendations', { topic, level, weeks });
    const plan = (data.plan || []).map((item, index) => `<li>${index + 1}. ${item}</li>`).join('');
    renderOutput('learn-output', `<ul>${plan}</ul>`);
  } catch (error) {
    renderOutput('learn-output', `<p class="error">${error.message}</p>`);
  }
});
