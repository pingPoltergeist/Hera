import {isAuthenticated} from "../../helpers/authApiCalls"
import {useEffect, useState} from "react"
import AdminNav from "../../components/admin/AdminNav"
import UserList from "../../components/admin/UserList";
import Fallback from "../../components/Fallback";
import {ErrorBoundary} from "react-error-boundary";

const users = () => {

    const token = isAuthenticated()

    return (
        <div className="admin_page">
            <AdminNav active="overview"/>

            <h1 className="admin_page_title">Hera Dashboard — Libraries</h1>
            <p className="admin_page_description">This is the user management page of the Hera dashboard. Here you can manage your users, add new user and delete existing users. To delete an user click on the cross button on the particular user card and to add an user, click on the add button.</p>

            <ErrorBoundary FallbackComponent={Fallback}>
                <UserList token={token}/>
            </ErrorBoundary>
        </div>
    )
}

export default users