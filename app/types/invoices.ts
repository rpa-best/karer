import type { DefaultQueryParams } from "."
import type { Car } from "./car"
import type { Driver } from "./driver"
import type { Nomenclature } from "./onec"

export interface InvoiceNomenclature {
    created_at: string
    nomenclature: string | null
    value: number
    invoice: number | undefined
}

export interface Invoice {
    id: number
    number: string
    created_at: string
    updated_at: string
    status: 'created' | 'process' | 'done' | 'canceled'
    address: string
    type: 'prepayment' | 'deferment_payment' | 'limit'
    comment: string
    org: string
    specification: string
    nomenclatures: InvoiceNomenclature[]
}

export interface InvoiceParams extends DefaultQueryParams {
    status?: 'all' |'created' | 'process' | 'done' | 'canceled' | undefined  
    type?: 'prepayment' | 'deferment_payment' | 'limit' | undefined
    org?: string | undefined
    specification?: string | undefined
}

export interface DriverComment {
    id: number
    status: 'loading' | 'ok' | 'error'
    text: string
    created_at: string
}

export interface Order {
    uuid: string
    car: Car
    driver: Driver
    nomenclature: Nomenclature
    invoice: number
    address: string
    per_price: number
    additive: number
    order: number
    fact: number
    done: boolean
    comment: string
    created_at: string
    updated_at: string
}

export interface OrderForm {
    uuid: string
    car: number
    driver: number
    nomenclature: string
    invoice: number
    address: string
    per_price: number
    additive: number
    order: number
    fact: number
    comment: string
    done: boolean
}

export interface Pivot {   
    current_summa: number
    results: Nomenclature[]
    summa: number  
}

export interface OrderParams extends DefaultQueryParams {}
