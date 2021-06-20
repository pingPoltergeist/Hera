import {API} from "../backend";

export const getRandomTv = (token) => {
    return fetch(`${API}/random-media/tv`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getTvList = (filter, count) => {
    let url = `${API}/tvs`
    if (filter){
        url +=`/${filter}`
    }
    if (count){
        url +=`/${count}`
    }
    return fetch(url)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getTvByID = (tvID, token) => {
    return fetch(`${API}/tv/${tvID}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}