import { render } from '@testing-library/react'
import '@testing-library/jest-dom'


require('jest-fetch-mock').enableMocks()
fetchMock.dontMock()

export const variables = {
    user: {
        "username": "subha",
        "password": "SK3un$@du",
        "loading": false,
        error: ""
    }
}
