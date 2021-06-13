import {signin} from "../authApiCalls";
import { variables } from '../../test/test-utils'

describe("Authentication", () => {
    it('should contain access token', async () => {
        const response = await signin(variables.user)
        expect(response.access).toBeTruthy()
    })
})