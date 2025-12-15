import { NextResponse } from "next/server"

export async function GET() {
  // Simulate some processing
  await new Promise((resolve) => setTimeout(resolve, 500))

  return NextResponse.json({
    message: "Hello from the API!",
    timestamp: new Date().toISOString(),
  })
}
