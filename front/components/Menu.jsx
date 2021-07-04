import styles from '/styles/components/Menu.module.scss'
import Link from "next/link";
import {Router, useRouter} from "next/router";
import {motion } from "framer-motion";
import {isAdmin, signout} from "../helpers/authApiCalls";
import {useState, useEffect} from "react";


const Menu = ({hamburgerFlag, setHamburgerFlag}) => {

    Router.events.on('routeChangeComplete', () => {
        setHamburgerFlag(false)
    })

    const router = useRouter()
    const [admin, setAdmin] = useState(false)

    useEffect(()=> {
        isAdmin().then(data => {
            setAdmin(data)
        })
    }, [])

    return (
        <motion.div key={'child'} className={styles.menu_container} initial={{opacity: 0}} animate={{opacity: 1}} exit={{ opacity: 0 }}>
            <div>
                {admin && <p className={styles.menu_link}><Link href="/settings">SETTINGS</Link></p>}
                <p className={styles.menu_link}><Link href="/favourites">FAVOURITES</Link></p>
                <p className={styles.menu_link} onClick={() => signout(() => {router.replace('/login')})}>LOG OUT</p>
            </div>
            <div>
                <img src="/hamburger_close.svg" onClick={() => {setHamburgerFlag(false)}} alt="close"/>
            </div>
            <div>
                <p className={styles.menu_link}><Link href="/">HOME</Link></p>
                <p className={styles.menu_link}><Link href="/collection">COLLECTIONS</Link></p>
                <p className={styles.menu_link}><Link href="/movie">MOVIES</Link></p>
                <p className={styles.menu_link}><Link href="/tv">SHOWS</Link></p>
            </div>
        </motion.div>
    )
}

export default Menu