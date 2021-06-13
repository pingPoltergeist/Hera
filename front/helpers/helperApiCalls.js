import {API} from "../backend";

export const search = (query) => {
    return fetch(`${API}/search?q=${query}`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getVideoByID = (videoID, token) => {
    return fetch(`${API}/movie/${videoID}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const sync = () => {
    return fetch(`${API}/sys/sync`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const addToWatchlist = (token, mediaID, seconds) => {
    let body = {
        "timestamp": seconds
    }
    return fetch(`${API}/user/watchlist/${mediaID}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
    })
        .then(response => {return response})
        .catch(err => console.log(err))
}

export const addDeleteFavourite = (token, mediaID, method) => {
    let body = {
        "tmdb_id": mediaID
    }
    return fetch(`${API}/user/wishlist/`, {
        method: `${method}`,
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(body)
    })
        .then(response => {return response})
        .catch(err => console.log(err))
}

export const getFavourites = (token) => {
    return fetch(`${API}/user/wishlist`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}
