import Image from 'next/image'
import { Inter } from 'next/font/google'
import { useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('host')

  const login = async () => {
    console.log(username, password, role)
    const res = await fetch('http://localhost:5000/login', {
      method: 'POST',
      body: JSON.stringify({ username, password, role }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await res.json()
    if(data.success) {
      localStorage.setItem('userId', data["id"])
      localStorage.setItem('role', role)
      window.location.href = '/'
    } else {
      alert('Failed to Login!')
    }
  }
  
  return (
    <div className='w-full flex flex-col items-center gap-2 p-10'>
      <input value = {username} onChange={ (e) => setUsername(e.target.value)}
        required className="border-solid border-2 rounded-md" placeholder='Username'/>
      <input value = {password} onChange={ (e) => setPassword(e.target.value)}
        required className="border-solid border-2 rounded-md" placeholder='Password'/>
      <div className="flex flex-row gap-1">
        <input onChange={ (e) => setRole(e.target.value)}
        type="radio" id="admin" name="role" value="host" />
        <label htmlFor="admin">Host</label>
        <input onChange={ (e) => setRole(e.target.value)}
         type="radio" id="host" name="role" value="renter" />
        <label htmlFor="host">Renter</label>
      </div>
      <button onClick={() => {login()}}
        className="border-solid border-2 rounded-md p-1">Login</button>
      <a href="/register">No account? Register!</a>
      <a href="/reports">BnB Reports</a>
    </div>
  )
}
