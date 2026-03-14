import { useState } from 'react'

export default function Home() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [contexts, setContexts] = useState([])

  async function ask() {
    const resp = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, top_k: 5 })
    })
    const data = await resp.json()
    setAnswer(data.answer)
    setContexts(data.contexts || [])
  }

  return (
    <main style={{ maxWidth: 900, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h1>RAG NL Platform</h1>
      <p>Ask questions over Dutch open datasets loaded into the RAG stack.</p>
      <textarea value={question} onChange={e => setQuestion(e.target.value)} rows={5} style={{ width: '100%' }} />
      <br />
      <button onClick={ask}>Ask</button>
      <h2>Answer</h2>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{answer}</pre>
      <h2>Contexts</h2>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(contexts, null, 2)}</pre>
    </main>
  )
}
