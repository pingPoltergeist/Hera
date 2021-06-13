import Signin from "../components/utils/SignIn"
import styles from '/styles/pages/Login.module.scss'
import {Fade, Modal} from "@material-ui/core"
import {useState} from "react"
import Fallback from "../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";

const login = () => {

    const [open, setOpen] = useState(false)

    const handleOpen = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
    }

    return (
        <div className={styles.container}>
            <div className={styles.content_box}>
                <img src="/logo.svg" className={styles.logo} alt=""/>
                <p className={styles.description_primary}>HERA is a home media server used to organize your collection of movies and tv shows. You add the location of your library and Hera organizes your content automatically and makes them available to everyone in your network</p>
                <button onClick={handleOpen} className={styles.login_button}>GET ALL THERE</button>
                <p className={styles.description_secondary}>Get Premier Access to Raya and the Last Dragon for an additional fee with a Disney+ subscription. As of 03/26/21, the price of Disney+ and The Disney Bundle will increase by $1.</p>
                <img src="/images/login_logo_two.png" className={styles.logo_two} alt=""/>
            </div>

            <Modal
                aria-labelledby="transition-modal-title"
                aria-describedby="transition-modal-description"
                className={styles.modal}
                open={open}
                onClose={handleClose}
                closeAfterTransition
                BackdropProps={{
                    timeout: 500,
                }}
            >
                <ErrorBoundary FallbackComponent={Fallback}>
                    <Fade in={open}>
                        <div className={styles.paper}>
                            <Signin />
                        </div>
                    </Fade>
                </ErrorBoundary>
            </Modal>
        </div>
    )
}

export default login