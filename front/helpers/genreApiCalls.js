import {API} from "../backend";

export const getAllGenres = () => {
    return fetch(`${API}/genre/`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getGenre = (genreID) => {
    return fetch(`${API}/genre/${genreID}`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}