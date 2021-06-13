import {withAuth} from "../helpers/utilities";

const NotFound = () => {
    return (
        <div>
            <h1>404 Not Found</h1>
        </div>
    )
}

export default withAuth(NotFound)