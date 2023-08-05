import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en" className='h-full w-full'>
      <Head />
      <body className='h-full w-full'>
        <div className="flex text-3xl justify-center w-full">
          <h1 className=""> Sample BnB Application</h1>
        </div>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
