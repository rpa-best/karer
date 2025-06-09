
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
    nomenclatures: string[]
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

export interface Driver {
    uuid: number
    name: string
    inn: string
    phone_number: string
    job_title: string
    drivers_license_series: string
    drivers_license_number: string

    telegram_id: string
    created_at: string
    image: string
}


export interface Car {
    uuid: number
    name: string
    reg_number: string
    brand: string
    our_prorerty: boolean
    trailer_reg_number: string
    trailer_brand: string

    not_weight: boolean
    created_at: string
    image: string
}