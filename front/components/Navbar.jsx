import styles from '/styles/components/Navbar.module.scss'
import Link from 'next/link'
import {useState} from "react";
import Menu from "./Menu";
import { AnimatePresence } from "framer-motion";
import Search from "./utils/Search";
import Sync from "./utils/Sync";

export default function Navbar() {

    const [hamburgerFlag, setHamburgerFlag] = useState(false)

    return (
        <div className={styles.navbar}>
            <div className={styles.left_section}>
                <div className={styles.hamburger} onClick={() => {
                    setHamburgerFlag(true)
                }}>
                    <div />
                    <div />
                    <div />
                </div>
                <ul className={styles.menu_block}>
                    <li><Link href="/">HOME</Link></li>
                    <li><Link href="/collection">COLLECTIONS</Link></li>
                    <li><Link href="/movie">MOVIES</Link></li>
                    <li><Link href="/tv">SHOWS</Link></li>
                </ul>
            </div>
            <div className={styles.right_section}>
                <Search />
                <Sync />
            </div>

            <AnimatePresence>
                {hamburgerFlag && <Menu hamburgerFlag={hamburgerFlag} setHamburgerFlag={setHamburgerFlag}/>}
            </AnimatePresence>
        </div>
    )
}