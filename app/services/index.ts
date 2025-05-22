import { CRUDService, ReadOnlyService } from "./utils";


export class CarService extends CRUDService {
    constructor() {
        super('/car/')
    }
}

export class DriverService extends CRUDService {
    constructor() {
        super('/driver/')
    }
}

export class NomenclatureService extends ReadOnlyService {
    constructor() {
        super('/onec/nomenclature/')
    }
}

export class OrganizationService extends ReadOnlyService {
    constructor() {
        super('/onec/organization/')
    }
}

export class SpecificationService extends ReadOnlyService {
    constructor() {
        super('/onec/specification/')
    }
}

export class OrderService extends ReadOnlyService {
    constructor() {
        super('/order/')
    }
}
