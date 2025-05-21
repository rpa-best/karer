
export interface Organization {
    uuid: string
    name: string
    fullname: string
    inn: string
    kpp: string
}


export interface Specification {
    uuid: string
    name: string
    delivery_address: string
    payment_deferment: number
    amount_limit: number
}


export interface Nomenclature {
    uuid: string
    per_price: number
    fact: number
    fact_current: number
    order_sum: number
    order_current_sum: number
    name: string
    unit: string
}