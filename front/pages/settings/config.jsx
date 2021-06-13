import AdminNav from "../../components/admin/AdminNav"
import styles from "../../styles/pages/settings/Config.module.scss"
import {isAuthenticated} from "../../helpers/authApiCalls";
import {useState} from "react";
import {changePort} from "../../helpers/settingsApiCalls";

const config = () => {

    const token = isAuthenticated()
    const [newPort, setNewPort] = useState('')

    const handleChange = (event) => {
        setNewPort(event.target.value)
    }

    const handleSubmit = () => {
        newPort !== '' && changePort(token, newPort).then(response => {return null})
    }

    return (
        <div className="admin_page">
            <AdminNav active="overview"/>

            <h1 className="admin_page_title">Hera Dashboard — Settings</h1>
            <p className="admin_page_description">This the miscellaneous settings page of the Hera dashboard. At this moment you can update the port number your Hera installation runs on. As we work on more feature they will be available on this page in the future.</p>

            <p className={styles.hera_version}>HERA  — v0.2.285019a</p>

            <form>
                <h1 className={styles.form_title}>Change port number</h1>
                <input required onChange={handleChange} type="number" placeholder="HERA port number" className={styles.single_folder_box}/>
                <button onClick={handleSubmit} className={styles.library_button} type="submit">Change port</button>
            </form>
        </div>
    )
}

export default config