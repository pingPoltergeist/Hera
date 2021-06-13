import {API} from "../backend";

export const getRandomMedia = (type, count) => {
    let url = `${API}/random-media`
    if (type){
        url +=`/${type}`
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

export const getMovieList = (filter, count) => {
    let url = `${API}/movies`
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

export const getAllMovies = () => {
    return fetch(`${API}/movies`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getMovieByID = (movieID, token) => {
    // console.log(token)
    return fetch(`${API}/movie/${movieID}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}