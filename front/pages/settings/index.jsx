import {withAdmin} from "../../helpers/utilities"
import styles from '/styles/pages/settings/Home.module.scss'
import Overview from "/components/admin/Overview"
import {isAuthenticated} from "../../helpers/authApiCalls"
import AdminNav from "../../components/admin/AdminNav";
import Fallback from "../../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";

const AdminHome = () => {

    const token = isAuthenticated()

    return (
        <div className="admin_page">
            <AdminNav active="overview"/>

            <h1 className="admin_page_title">Hera Dashboard — Overview</h1>
            <p className="admin_page_description">This is the overview page of your Hera installation. You will find some at a glace information about your library and your contents. Just above this section there is a navigation menu which you can use to navigate between multiple pages of this dashboard.</p>

            <ErrorBoundary FallbackComponent={Fallback}>
                <Overview token={token}/>
            </ErrorBoundary>
        </div>
    )
}

export default withAdmin(AdminHome)
