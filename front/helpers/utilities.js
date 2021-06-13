import { useRouter } from "next/router"
import {isAdmin} from "./authApiCalls";
import {API} from "../backend";

export const shorten = (string) => {
    if (!string) {
        return
    }

    let shortenedString = string.substr(0, 400)
    if (shortenedString.length === 400) {
        let re = /\.\s[A-Z]/
        shortenedString = shortenedString.substr(0, Math.min(shortenedString.length, shortenedString.lastIndexOf('. '))) + ' . . .'
    }
    return shortenedString
}

export const withAuth = (WrappedComponent) => {
    return (props) => {
        if (typeof window !== "undefined") {
            const Router = useRouter()
            const token = localStorage.getItem("jwt")

            if (!token) {
                Router.replace("/login");
                return null
            }

            return <WrappedComponent {...props} />
        }

        return null
    }
}

export const withAdmin = (WrappedComponent) => {
    return (props) => {
        if (typeof window !== "undefined") {
            const Router = useRouter()

            isAdmin().then(admin => {
                if (!admin) {
                    Router.replace("/")
                    return null
                }
            })
            return <WrappedComponent {...props} />

        }

        return null
    }
}

String.prototype.toTitleCase = function() {
    return this.charAt(0).toUpperCase() + this.slice(1)
}