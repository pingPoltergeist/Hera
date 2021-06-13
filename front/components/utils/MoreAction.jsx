import styles from '/styles/components/utils/MoreAction.module.scss'
import {motion } from "framer-motion";
import {useEffect, useState} from "react";
import {isAdmin, isAuthenticated} from "../../helpers/authApiCalls";
import {addDeleteFavourite} from "../../helpers/helperApiCalls";
import {Fade, Modal} from "@material-ui/core";
import {useRouter} from "next/router";
import {changeTmdbID} from "../../helpers/settingsApiCalls";

const MoreAction = ({media, flag, setFlag, type}) => {

    const [admin, setAdmin] = useState(false)
    const token = isAuthenticated()
    const router = useRouter()
    const [changedID, setChangedID] = useState('')

    useEffect(()=> {
        isAdmin().then(data => {
            setAdmin(data)
        })
    }, [])

    const [open, setOpen] = useState(false)

    const handleOpen = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
    }

    const handleFavourite = (method) => {
        addDeleteFavourite(token, media.tmdb_id, method).then(response => {
            media.favourite = !media.favourite
            return null
        })
    }

    const handleChange = event => {
        setChangedID(parseInt(event.target.value))
    }

    const onSubmit = event => {
        event.preventDefault()
        changeTmdbID(token, media.tmdb_id, type, changedID).then(response => {return null})
        setFlag(false)
        router.replace('/').then(value => router.reload())
    }

    return (
        <motion.div className={styles.more_action_container}
            initial={{opacity: 0, y: '-90%', x: -10}}
            animate={{opacity: 1, y: '-110%', x: 0}}
            exit={{ opacity: 0, y: '-90%', x: -10 }}
            transition={{ type: "tween" , duration: 0.2}}
            onMouseLeave={() => {
                setTimeout(() => setFlag(false), 500)
            }}
        >
            {!media.favourite
                ? <p onClick={() => {handleFavourite('POST'); setFlag(false)}} className={styles.more_action_link}>Add to favourites</p>
                : <p onClick={() => {handleFavourite('DELETE'); setFlag(false)}} className={styles.more_action_link}>Remove from favourite</p>
            }
            {admin && type !== 'collection' && <p onClick={handleOpen} className={styles.more_action_link}>Change TMDB ID</p>}

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
                <Fade in={open}>
                    <div className={styles.paper}>
                        <div className="form_block">
                            <h1 className="form_title">Change TMDB ID of {type}</h1>

                            <input onChange={handleChange} value={changedID} placeholder="New TMDB ID" className="form-input" type="text" />

                            <button onClick={onSubmit} type="submit" className="button">Change TMDB ID</button>
                        </div>
                    </div>
                </Fade>
            </Modal>
        </motion.div>
    )
}

export default MoreAction