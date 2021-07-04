import Head from "next/head";
import Navbar from "./Navbar";
import {Router, useRouter} from "next/router";
import NProgress from 'nprogress'
import screenfull from "screenfull";

Router.events.on('routeChangeStart', (url) => {
    NProgress.start()
})

Router.events.on('routeChangeComplete', () => {
    NProgress.done()
    screenfull.exit()
})

Router.events.on('routeChangeError', () => {
    NProgress.done()
})


const Base = ({children}) => {

    const router = useRouter()

    return (
        <div>
            <Head>
                <title>HERA | Home Media Server</title>
                <link rel="icon" href="/favicon.ico" />

            </Head>
            {router.pathname !== '/login' && router.pathname !== '/watch/[videoID]' && <Navbar />}
            {children}
        </div>
    )
}

export default Base