"use client"

import { Button } from "@/components/ui/button"
import { useState } from "react"

export default function Page() {
  const [response, setResponse] = useState<string>("")
  const [loading, setLoading] = useState(false)

  const handleClick = async () => {
    setLoading(true)
    setResponse("")

    try {
      const res = await fetch("/api/hello")
      const data = await res.json()
      setResponse(data.message)
    } catch (error) {
      setResponse("Error calling API")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-background">
      <div className="flex flex-col items-center gap-4">
        <Button onClick={handleClick} disabled={loading} className="min-w-32">
          {loading ? "Loading..." : "Call API"}
        </Button>

        {response && <p className="text-sm text-muted-foreground">{response}</p>}
      </div>
    </main>
  )
}
