import Image from 'next/image'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function Login() {
  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <input className="border-solid border-2 rounded-md" placeholder='Username'/>
      <input className="border-solid border-2 rounded-md" placeholder='Password'/>
      <button className="border-solid border-2 rounded-md p-1">Login</button>
      <a href="/register">No account? Register!</a>
      <a href="/reports">BnB Reports</a>
    </div>
  )
}
