import styles from '/styles/components/admin/AdminNav.module.scss'
import Link from "next/link"

const AdminNav = ({active}) => {

    return (
        <div className={styles.nav_container}>
            <ul className={styles.menu_block}>
                <li id="overview"><Link href="/settings">OVERVIEW</Link></li>
                <li id="libraries"><Link href="/settings/libraries">LIBRARIES</Link></li>
                <li id="users"><Link href="/settings/users">USERS</Link></li>
                <li id="settings"><Link href="/settings/config">SETTINGS</Link></li>
            </ul>
        </div>
    )
}

export default AdminNav