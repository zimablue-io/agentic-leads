import { AlertCircle } from 'lucide-react'

export default function SetupMessage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[#161616]">
      <div className="w-full max-w-md border border-[#333333] rounded-md p-4 text-center">
        <AlertCircle className="mx-auto h-8 w-8 text-yellow-500" />
        <h1 className="text-2xl font-bold mb-4 text-white">Connect Supabase to get started</h1>
        <p className="text-sm text-gray-500">
          To use the features of this app, you need to connect to your Supabase project.
        </p>
      </div>
    </div>
  )
}
