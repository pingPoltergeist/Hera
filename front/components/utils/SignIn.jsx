import {useState} from 'react'
import {authenticate, isAuthenticated, signin} from "../../helpers/authApiCalls";
import styles from '/styles/components/utils/Sigin.module.scss'
import {useRouter} from "next/router";
import Alert from './Alert'

const Signin = () => {

    const [user, setUser] = useState({
        username: 'subha',
        password: 'SK3un$@du',
        loading: false,
        error: ''
    })

    const handleChange = name => event => {
        setUser({...user, [name]: event.target.value})
    }

    const router = useRouter()

    const onSubmit = event => {
        event.preventDefault()
        setUser({...user, loading: true, error: ''})
        signin(user)
            .then(data => {
                if (data) {
                    authenticate(data, () => {
                        setUser({...user, username: '', password: '', loading: false, error: ''})
                    })
                } else {
                    setUser({...user, loading: false, error: 'Could not sign in'})
                }
            })
    }

    const performRedirect = () => {
        if (isAuthenticated()) {
            router.replace('/')
        }
    }

    return (
        <div className="form_block">
            <img src="/logo.svg" className="form_logo" alt=""/>
            <h1 className="form_title">Sign in to get access</h1>

            <input onChange={handleChange('username')} value={user.username} placeholder="Username" className="form-input" type="text" />
            <input onChange={handleChange('password')} value={user.password} placeholder="Password" className="form-input" type="password" />

            <button onClick={onSubmit} type="submit" className="button">Sign In</button>

            {user.error && <Alert severity="error" message={user.error}/>}
            {performRedirect()}
        </div>
    )
}

export default Signin
