export interface Notification {
    id: number,
    label: string
    message: string
    redirect_url: string
    read: boolean
    created_at: string
    read_at: string
    severity: string
}