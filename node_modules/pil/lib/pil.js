// PIL lib
'use strict';

/**
 * Example parameter schema
 * {
 *     name: String,         // Name of your parameter - Required
 *     required: Boolean,    // Required if true, optional if false - true by default
 *     type: String,         // Parameter data type; boolean | number | string | object | array
 *     regex: Object (regex) // Regular expression to match with if parameter is string.
 *     error: {              // Set custom error messages in specific scenarios
 *         missing: String,
 *         incorrectType: String,
 *         regexMatch: String
 *     }
 * }
 */

// Internal library
const url = require('url')

/*
* Main pil function
*/
function pil () {}

/*
* Main util function
*/
function util () {}

/**
 * Util - Check the parameter type to make sure it fits options
 *
 * Returns true | false on success | failure
 */
util.checkType = function (type,val) {
    let typeValid = false

    // Check for types
    switch (type) {
        // - string is straight-forward
        case "string":
            if (typeof(val) === "string") {
                typeValid = true
            }
            break

        // - number needs parsing
        case "number":
            if (parseInt(val) !== NaN) {
                typeValid = true
            }
            break

        // - arrays are objects in js so we can check length
        case "array":
            if (typeof(val) === "object" && parseInt(val.length) !== NaN) {
                typeValid = true
            }
            break

        // - simple objects are straight-forward
        case "object":
            if (typeof(val) === "object") {
                typeValid = true
            }
            break

        // - bools are straight-forward
        case "boolean":
            if (typeof(val) === "boolean") {
                typeValid = true
            }
            break

        default:
            if (typeof(val) === paramOpt.type) {
                typeValid = true
            }
            break
    }

    return typeValid
}

/**
 * Util - Translates http quries/body-parsed into an universal object
 *
 * Returns parameters as an object
 *
 * TODO: Checking for non-bodyparsed requests on POST/PUT
 */
util.params = function (req) {
    // Check for method types to catch parameters
    if (req.method === 'GET' || req.method === 'DELETE') {
        return url.parse(req.url, true).query
    } else if (req.method === 'POST' || req.method === 'PUT') {
        // Check that body is in this.req
        if (!req.body) {
            throw new Error('no body found for this ' + req.method + ' method, please use koa-bodyparser (or similar) in your koa app.')
        }
        return req.body
    }
}

/**
 * Util - Translates http quries/body-parsed into an universal object
 *
 * Returns value
 */
util.regex = function (opts,val) {
    // Check that parameter is string
    if (opts.type === 'string' && typeof(val) === 'string') {

        // Run match
        let match = val.match(opts.regex)

        if (match) {
            return true
        } else {
            return false
        }
    } else {
        return true
    }
}

/**
 * pil - Middleware generator that will set parameters
 *
 * Sets params into context this.request.params
 */
pil.set = function (opts) {
    // Class variables to set
    let params = {}

    // Check params
    return function * (next) {
        // Flush ctx params
        this.request.params = {}

        try {
            params = util.params(this.request)
        } catch (error) {
            this.throw(500, error)
        }

        // Run through options
        for (let paramOpt of opts) {

            // Make sure options are correct
            if (!paramOpt.name) {
                this.throw(500, "Parameter must have a name.")
            }
            if (!paramOpt.type) {
                paramOpt.type = "string"
            }

            // Set variables
            let required = null,
                error = null

            // Check for required
            if (paramOpt.required !== undefined) {
                required = paramOpt.required
            } else {
                required = true
            }

            let keys = Object.keys(params)

            // Check that parameter exists
            if (keys.indexOf(paramOpt.name) !== -1) {

                // Set key
                let k = keys[keys.indexOf(paramOpt.name)]
                let v = params[k]

                // Match parameters
                if (k === paramOpt.name) {

                    // Checking parameter type
                    let typeValid = util.checkType(paramOpt.type,v)

                    // Run regex check if needed
                    let regexValid = util.regex(paramOpt,v)

                    // Check for type
                    if (!typeValid) {
                        // Set error message
                        if (paramOpt.error && paramOpt.error.incorrectType) {
                            error = paramOpt.error.incorrectType
                        } else {
                            error = paramOpt.name + " parameter needs to be a " + paramOpt.type + " not a " + typeof(v) + "."
                        }
                        // Error for missing parameters
                        this.throw(400, error)
                    } else if (!regexValid && paramOpt.regex) {
                        // Set error message
                        if (paramOpt.error && paramOpt.error.regexMatch) {
                            error = paramOpt.error.regexMatch
                        } else {
                            error = paramOpt.name + " does not validate with this regular expression; " + paramOpt.regex
                        }
                        // Error for missing parameters
                        this.throw(400, error)
                    } else {
                        // Set into request context
                        this.request.params = params
                    }
                }

            } else if (required === true) {
                // Set error message
                if (paramOpt.error && paramOpt.error.missing) {
                    error = paramOpt.error.missing
                } else {
                    error = "You need to provide the " + paramOpt.name + " parameter to this endpoint."
                }
                // Error for missing parameters
                this.throw(400, error)
            }
        }

        if (next) yield next
    }
}

module.exports = pil