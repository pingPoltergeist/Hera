import {useEffect, useState} from "react"
import {changeTmdbID, createUser, deleteUser, getAllUsers} from "../../helpers/settingsApiCalls"
import styles from '/styles/components/admin/UserList.module.scss'
import {useRouter} from "next/router"
import {Fade, Modal} from "@material-ui/core";

const UserList = ({token}) => {

    const router = useRouter()
    const [users, setUsers] = useState([])
    const [newUser, setNewUser] = useState({
        username: '',
        password: '',
        age: '',
        firstname: '',
        lastname: ''
    })
    const [open, setOpen] = useState(false)

    const handleOpen = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
    }

    const preload = () => {
        getAllUsers(token).then(response => setUsers(response))
    }

    useEffect(() => {
        preload()
    }, [])

    const handleDelete = (username) => {
        deleteUser(token, username).then(response => {return null})
        router.reload()
    }

    const handleChange = name => event => {
        setNewUser({...newUser, [name]: event.target.value})
    }

    const handleSubmit = event => {
        event.preventDefault()
        createUser(token, newUser).then(response => {return null})
        setOpen(false)
        router.reload()
    }


    return (
        <div className={styles.user_list_container}>
            {users.map((user, index) => (
                <div key={index} className={styles.single_user_container}>
                    <img src="/images/default_user.png" alt="user" className={styles.single_user_picture}/>
                    <h3 className={styles.single_user_username}>{user.username}</h3>
                    <p className={styles.single_user_fullname}>{user.fullname}</p>

                    {!user.is_superuser && <img onClick={() => handleDelete(user.username)} className={styles.delete_user_button} src="/images/utils/delete_user.svg" alt="delete user"/>}
                </div>
            ))}

            <div className={styles.single_user_container}>
                <img className={styles.new_user_button} onClick={handleOpen} src="/images/utils/add_user.svg" alt=""/>
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
                <Fade in={open}>
                    <div className={styles.paper}>
                        <div className="form_block">
                            <h1 className="form_title">Create a new user</h1>

                            <input required onChange={handleChange('username')} value={newUser.username} placeholder="Username" className="form-input" type="text" />
                            <input required onChange={handleChange('password')} value={newUser.password} placeholder="Password" className="form-input" type="password" />
                            <input required onChange={handleChange('age')} value={newUser.age} placeholder="Age" className="form-input" type="text" />
                            <input required onChange={handleChange('firstname')} value={newUser.firstname} placeholder="First Name" className="form-input" type="text" />
                            <input required onChange={handleChange('lastname')} value={newUser.lastname} placeholder="Last Name" className="form-input" type="text" />

                            <button onClick={handleSubmit} type="submit" className="button">Create new user</button>
                        </div>
                    </div>
                </Fade>
            </Modal>
        </div>
    )
}

export default UserList