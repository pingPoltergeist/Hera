import {API} from "../backend";

export const getAllCollections = () => {
    return fetch(`${API}/movie-collection-list/`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getCollectionByID = (collectionID) => {
    return fetch(`${API}/movie-collection/${collectionID}`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}

export const getRandomCollection = () => {
    return fetch(`${API}/random-collection`)
        .then(response => {
            return response.json()
        })
        .catch(err => console.log(err))
}