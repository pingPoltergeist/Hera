import {API} from "../backend";
import Cookies from "cookies";

export const signin = (user) => {
    return fetch(`${API}/user/token/`, {
        method: "POST",

        headers: {
            Accept: "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
    })
        .then(response => {
            return response.json()
        })
        .catch(err => {console.log(err);})
}



export const authenticate = (data, next) => {
    if (typeof window !== "undefined") {
        if (data && data.access) {
            localStorage.setItem("jwt", JSON.stringify(data.access))

            let date = new Date()
            date.setTime(date.getTime()+(30*24*60*60*1000))
            let expiry = date.toUTCString()

            document.cookie = `jwt=${JSON.stringify(data.access)}; expires=${expiry}; path=/`
        } else {
            throw 'Failed to authenticate'
        }
        next()
    }
}



export const signout = (next) => {
    if (typeof window !== "undefined") {
        localStorage.removeItem("jwt")
        next()
    }
}

export const isAuthenticated = () => {
    if (typeof window == "undefined") {
        return false
    }

    if (localStorage.getItem("jwt")) {
        return JSON.parse(localStorage.getItem("jwt"))
    }

    else {
        return false
    }
}

export const isAdmin = () => {
    if (typeof window === "undefined") {
        return false
    }

    if (localStorage.getItem("jwt")) {
        const token = JSON.parse(localStorage.getItem("jwt"))
        return fetch(`${API}/user/profile`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }).then(data => data.json())
            .then(data =>{
            return !!data.is_superuser
        }).catch(err => {
            console.log(err)
            return false
        })
    }
}

export const getCookieToken = (req, res) => {
    const cookies = new Cookies(req, res)
    return cookies.get('jwt').replace(/^"(.*)"$/, '$1')
}