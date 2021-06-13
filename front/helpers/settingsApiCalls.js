import {API} from "../backend";

export const getCount = (token, item) => {
    return fetch(`${API}/sys/count/${item}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const changeTmdbID = (token, mediaID, type, newID) => {
    return fetch(`${API}/change-tmdb-id/${type}/${mediaID}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
            "new_tmdb_id": newID
        })
    })
        .then(response => {return response})
        .catch(err => console.log(err))
}

export const getMediaFolders = (token) => {
    return fetch(`${API}/sys/media-folders/`, {
        headers: {
            Authorization: `Bearer ${token}`,
        }
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}

export const handleMediaFolder = (token, folder, type, method) => {
    return fetch(`${API}/sys/media-folders/${type}/`, {
        method,
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "dir": folder
        })
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}

export const getAllUsers = (token) => {
    return fetch(`${API}/user/`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}

export const deleteUser = (token, username) => {
    return fetch(`${API}/user`, {
        method: 'DELETE',
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username
        })
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}

export const createUser = (token, newUser) => {
    return fetch(`${API}/user/`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(newUser)
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}

export const changePort = (token, newPort) => {
    return fetch(`${API}/sys/port/`, {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            port: newPort
        })
    })
        .then(response => {return response.json()})
        .catch(err => console.log(err))
}