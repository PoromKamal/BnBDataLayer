import { useState } from "react"

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [sin, setSin] = useState('')
  const [name, setName] = useState('')
  const [dob, setDob] = useState('')
  const [address, setAddress] = useState('')
  const [occupation, setOccupation] = useState('')
  const [role, setRole] = useState('')

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    console.log(username, password, sin, name, dob, address, occupation, role)
  }

  return (
    <div className='w-full' >
      <form onSubmit={handleSubmit}
        className="flex flex-col items-center gap-2 p-10">
        <input value={username} onChange={e => setUsername(e.target.value)} 
          required className="border-solid border-2 rounded-md" placeholder='Username'/>
        <input value={password} onChange={e => setPassword(e.target.value)}
          required className="border-solid border-2 rounded-md" placeholder='Password'/>
        <input value={sin} onChange={e => setSin(e.target.value)}
          required className="border-solid border-2 rounded-md" placeholder='SIN'/>
        <input value={name} onChange={e => setName(e.target.value)}
          required className="border-solid border-2 rounded-md" placeholder='Name'/>
        <div>
          <label htmlFor="dob">Date of Birth: </label>
          <input value={dob} onChange={e => setDob(e.target.value)}
            required type="date" className="border-solid border-2 rounded-md" placeholder='Date of Birth'/>
        </div>
        
        <input value={address} onChange={e => setAddress(e.target.value)}
          required className="border-solid border-2 rounded-md" placeholder='Address'/>
        <input value={occupation} onChange={e => setOccupation(e.target.value)}
          required className="border-solid border-2 rounded-md" placeholder='Occupation'/>
        <div className="flex gap-2">
          <label htmlFor="role">Role: </label>
          <input onChange={e => setRole(e.target.value)}
            type="radio" id="host" name="role" value="host"/>
          <label htmlFor="host">Host</label>
          <input onChange={e => setRole(e.target.value)}
            type="radio" id="renter" name="role" value="renter"/>
          <label htmlFor="renter">Renter</label>
        </div>
        <button type="submit" className="border-solid border-2 rounded-md p-1">Register</button>
      </form>
    </div>
  )
}
